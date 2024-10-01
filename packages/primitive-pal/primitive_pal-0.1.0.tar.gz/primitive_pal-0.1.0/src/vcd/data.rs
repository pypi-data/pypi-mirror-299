use arrow::array::{
    ArrayRef, ListBuilder, RecordBatch, StringBuilder, StructBuilder, UInt64Array, UInt64Builder,
};
use arrow::datatypes::{DataType, Field, Schema};
use crossbeam_channel::unbounded; // TODO: Implement writer using crossbeam channels
use log::info;
use parquet::arrow::ArrowWriter;
use parquet::file::properties::WriterProperties;
use rayon::iter::IntoParallelIterator;
use rayon::prelude::*;
use std::collections::hash_map::Entry;
use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io::{self, Read, Seek, SeekFrom};
use std::os::unix::fs::FileExt;
use std::path::Path;
use std::sync::{Arc, Mutex};
use std::thread::{self};
use std::time::Instant;

use crate::vcd::parser::{Command, Parser};
use parquet::data_type::AsBytes;

#[derive(Debug, Copy, Clone)]
struct DataChunk {
    start: u64,
    end: u64,
}

pub fn process_data(path: &Path, ptr: u64) -> io::Result<String> {
    // Extract filename
    let filename = match path.file_name() {
        Some(name) => format!("{}.parquet", name.to_string_lossy().into_owned()),
        None => "vcd.parquet".to_string(),
    };

    // Create chunks
    let appx_chunk_size = 1 * 1024 * 1024; // 1 MB approximate chunk size... 9GB in ~55s on 16 cores
    let chunks = create_chunks(path, ptr, appx_chunk_size)?;

    // Create file Mutex
    let file = Arc::new(Mutex::new(File::open(path)?));

    // Create Parquet file and schema
    let value_entry = vec![
        Field::new("id", DataType::UInt64, false),
        Field::new("value", DataType::Utf8, false),
    ];

    let schema = Arc::new(Schema::new(vec![
        Field::new("timestamp", DataType::UInt64, false),
        Field::new(
            "values",
            DataType::List(Arc::new(Field::new(
                "value",
                DataType::Struct(value_entry.into()),
                false,
            ))),
            false,
        ),
    ]));

    // Utilize crossbeam channel to send parallel reads to serial write thread
    let (tx, rx) = unbounded();
    let schema_clone = schema.clone();
    let writer_thread = thread::spawn(move || -> Result<(), Box<dyn Error + Send + Sync>> {
        let parquet_file = File::create(filename)?;
        let props = WriterProperties::builder().build();
        let mut writer = ArrowWriter::try_new(parquet_file, schema_clone.clone(), Some(props))?;

        for batch in rx {
            writer.write(&batch)?;
        }

        writer.close()?;
        Ok(())
    });

    let _ = (0..chunks.len()).into_par_iter().try_for_each_with(
        tx.clone(),
        |tx, i| -> Result<(), Box<dyn Error + Send + Sync>> {
            let now = Instant::now();
            // Local copy of file's Arc
            let file = Arc::clone(&file);
            let chunk_range = chunks[i];
            let buf_size = chunk_range.end - chunk_range.start;
            let mut buffer = vec![0u8; buf_size as usize];

            // Each thread reads its respective chunk
            {
                let mut file = file.lock().unwrap();
                file.seek(SeekFrom::Start(chunk_range.start))
                    .expect("Failed to seek");
                let bytes_read = file.read(&mut buffer).expect("Failed to read");
                buffer.truncate(bytes_read);
            }

            // Process each chunk
            {
                let mut parser = Parser::new(buffer.as_slice(), true);
                let mut current_timestamp = 0;

                let mut data_map: HashMap<u64, Vec<(u64, String)>> = HashMap::new();
                let mut append_value = |key: u64, id: u64, value: String| match data_map.entry(key)
                {
                    Entry::Occupied(mut e) => {
                        e.get_mut().push((id, value));
                    }
                    Entry::Vacant(e) => {
                        e.insert(vec![(id, value)]);
                    }
                };

                while let Ok(Some(command)) = parser.next().transpose() {
                    match command {
                        Command::Timestamp(t) => current_timestamp = t,
                        Command::ChangeScalar(id, value) => {
                            append_value(current_timestamp, id.into(), value.to_string())
                        }
                        Command::ChangeVector(id, value) => {
                            append_value(current_timestamp, id.into(), value.to_string())
                        }
                        Command::ChangeReal(id, value) => {
                            append_value(current_timestamp, id.into(), value.to_string())
                        }
                        command => println!(
                            "Unexpected {command:?} at line {line}",
                            line = parser.line()
                        ),
                    }
                }

                let id_builder = UInt64Builder::new();
                let value_builder = StringBuilder::new();
                let value_entry_fields = vec![
                    Field::new("id", DataType::UInt64, false),
                    Field::new("value", DataType::Utf8, false),
                ];
                let struct_builder = StructBuilder::new(
                    value_entry_fields.clone(),
                    vec![
                        Box::new(id_builder) as Box<dyn arrow::array::ArrayBuilder>,
                        Box::new(value_builder) as Box<dyn arrow::array::ArrayBuilder>,
                    ],
                );
                let list_element_field =
                    Field::new("value", DataType::Struct(value_entry_fields.into()), false);
                let mut list_builder =
                    ListBuilder::new(struct_builder).with_field(list_element_field);

                for (timestamp, values) in data_map.into_iter() {
                    let timestamp_array = UInt64Array::from(vec![timestamp]);
                    let struct_builder = list_builder.values();

                    for (id, value) in values.into_iter() {
                        struct_builder
                            .field_builder::<UInt64Builder>(0)
                            .unwrap()
                            .append_value(id);
                        struct_builder
                            .field_builder::<StringBuilder>(1)
                            .unwrap()
                            .append_value(value);
                        // Indicate that the struct is complete
                        struct_builder.append(true);
                    }

                    list_builder.append(true);
                    let values_list_array = list_builder.finish();
                    let columns: Vec<ArrayRef> =
                        vec![Arc::new(timestamp_array), Arc::new(values_list_array)];

                    let batch = RecordBatch::try_new(schema.clone(), columns).unwrap();

                    tx.send(batch).unwrap();
                }
            }

            println!("CHUNK TIME: {:.02?}", now.elapsed());

            Ok(())
        },
    );

    drop(tx);

    let _ = writer_thread.join().unwrap();

    Ok("success".to_string())
}

fn create_chunks(path: &Path, ptr: u64, appx_chunk_size: u64) -> io::Result<Vec<DataChunk>> {
    // Open file and seek to data section
    info!("Beginning chunk creation");
    let mut file = File::open(path)?;
    let file_size = file.metadata()?.len();
    let read_size = 10 * 1024 * 1024; // Read last 10 MB of the file
    let mut position: u64 = if read_size <= file_size && file_size - read_size > ptr {
        file_size - read_size
    } else {
        ptr
    };

    info!("Starting position: {position}");

    let mut chunks: Vec<DataChunk> = Vec::new();
    let mut buffer = [0u8, 2];

    // Seek to the first timestamp
    // TODO: Maybe we should check if the whole file is less than read size to read entire data array
    // Using this approach, the initial values are always left out
    while let Ok(bytes_read) = file.read_at(&mut buffer, position) {
        if bytes_read == 0 || buffer.as_bytes() == b"\n#" || buffer.as_bytes() == b"\r#" {
            break;
        }
        position += 1;
    }

    info!("Found first timestamp at {position}");

    while position < file_size {
        let start = position;
        let mut end = position + appx_chunk_size;
        file.seek(SeekFrom::Start(end))?;

        // Read bytes by two at end until signature is found
        while let Ok(bytes_read) = file.read_at(&mut buffer, end) {
            if bytes_read == 0 {
                // EOF reached, just break and extend the chunk to EOF
                break;
            }

            // Check for byte signature
            if buffer.as_bytes() == b"\n#" || buffer.as_bytes() == b"\r#" {
                // signature matches, end of chunk should be previous byte
                end -= 1;
                break;
            }

            // Move up position by one byte
            end += 1;
        }

        // Create new chunk
        chunks.push(DataChunk { start, end });

        // Set the new position to end + 1
        position = end + 1;
    }

    info!("File successfully chunked");
    Ok(chunks)
}
