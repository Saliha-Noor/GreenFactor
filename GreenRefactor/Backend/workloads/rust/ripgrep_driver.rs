// Workload driver for ripgrep — crates/core/main.rs
// Uses ripgrep binary (cargo build --release in the ripgrep repo)
// This is a shell-level driver: we build the binary and search a file.
// For the pipeline, the RustAdapter's build() does `cargo build --release`
// and run_once() calls the binary.
//
// This file exists as documentation of the workload args.
// Actual execution: <ripgrep_binary> "pattern" <target_file>
//
// Since ripgrep needs a target file to search, the driver creates one.

use std::fs;
use std::io::Write;

fn main() {
    // Create a sample file to search
    let sample = (0..10000)
        .map(|i| format!("line {} contains data item_{} with value {}", i, i % 100, i * 7))
        .collect::<Vec<_>>()
        .join("\n");
    
    let path = std::env::temp_dir().join("greenrefactor_rg_sample.txt");
    fs::write(&path, &sample).expect("Failed to write sample file");
    
    // Search for a pattern
    let contents = fs::read_to_string(&path).expect("Failed to read");
    let mut count = 0;
    for line in contents.lines() {
        if line.contains("item_42") {
            count += 1;
        }
    }
    
    println!("OK: searched {} lines, found {} matches", 10000, count);
    let _ = fs::remove_file(&path);
}
