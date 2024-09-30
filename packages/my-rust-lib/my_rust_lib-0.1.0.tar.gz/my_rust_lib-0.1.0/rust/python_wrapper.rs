use pyo3::prelude::*;
use crate::rust_impl::add as core_add; // Import the Rust implementation

/// A Python-exposed function that calls the core Rust implementation.
#[pyfunction]
fn add(a: usize, b: usize) -> PyResult<usize> {
    Ok(core_add(a, b))
}

/// A Python module implemented in Rust.
#[pymodule]
fn my_rust_lib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(add, m)?)?;
    Ok(())
}
