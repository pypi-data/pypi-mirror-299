use std::path::PathBuf;
use klarfrs::parse_internal;
use klarfrs::parse_defect_records;
fn main() -> std::io::Result<()> {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push("tests");
    path.push("klarf01.txt");
    
    let klarfrs = parse_internal(path.to_str().unwrap()).unwrap();

    let defects = parse_defect_records(path.to_str().unwrap()).unwrap();

    println!("{:#?}", klarfrs);
    Ok(())
}