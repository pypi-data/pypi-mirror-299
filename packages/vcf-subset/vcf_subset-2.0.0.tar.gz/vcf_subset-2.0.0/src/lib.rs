use std::{
    fs::File,
    io::{BufRead, BufReader},
};

use pyo3::prelude::*;

/// Subset a VCF file by a list of positions.
///
/// # Arguments
/// vcf_path: String - Path to the VCF file.
/// positions: Vec<u64> - List of positions to subset the VCF file by.
///
/// # Returns
/// Tuple of two lists of strings. The first list contains the header lines of the VCF file, and the second list contains the subsetted VCF lines.
#[pyfunction]
fn subset_vcf(vcf_path: String, positions: Vec<u64>) -> (Vec<String>, Vec<String>) {
    let file = File::open(vcf_path).unwrap();
    let reader = BufReader::new(file);
    let mut header = Vec::new();
    let mut output = Vec::new();

    for line in reader.lines() {
        let line = line.unwrap();
        if line.starts_with("#") {
            header.push(line);
        } else {
            let mut fields = line.split("\t");
            let pos = fields.nth(1).unwrap().parse::<u64>().unwrap();
            if positions.is_empty() || positions.contains(&pos) {
                output.push(line);
            }
        }
    }

    (header, output)
}

/// A Python module implemented in Rust.
#[pymodule]
fn vcf_subset(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(subset_vcf, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_subset_vcf() {
        let vcf_path = "test_data/test.vcf".to_string();

        // None of these positions lie in the VCF, so nothing should be returned
        let positions = vec![1, 2, 3, 4, 5];
        let (header, output) = subset_vcf(vcf_path.clone(), positions);

        assert_eq!(header.len(), 19);
        assert_eq!(output.len(), 0);

        let positions = vec![1043, 2, 3, 4, 5];
        let (header, output) = subset_vcf(vcf_path.clone(), positions);

        assert_eq!(header.len(), 19);
        assert_eq!(output.len(), 1);

        let positions = vec![1043, 1815, 1977, 4, 5];
        let (header, output) = subset_vcf(vcf_path.clone(), positions);

        assert_eq!(header.len(), 19);
        assert_eq!(output.len(), 3);

        let positions = vec![1043, 1815, 1977];
        let (header, output) = subset_vcf(vcf_path.clone(), positions);

        assert_eq!(header.len(), 19);
        assert_eq!(output.len(), 3);

        // No positions should return all rows
        let positions = vec![];
        let (header, output) = subset_vcf(vcf_path.clone(), positions);

        assert_eq!(header.len(), 19);
        assert_eq!(output.len(), 9);
    }
}
