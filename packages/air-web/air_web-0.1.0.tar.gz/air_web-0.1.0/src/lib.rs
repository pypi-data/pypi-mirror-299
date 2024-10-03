use html2text::from_read_with_decorator;
use pyo3::prelude::*;

mod decorator;

/// Converts HTML to Markdown.
#[pyfunction]
fn to_markdown(text: &str) -> String {
    from_read_with_decorator(
        text.as_bytes(),
        usize::MAX,
        decorator::CustomDecorator::new(),
    )
}

#[pymodule]
fn air_web(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(to_markdown, m)?)?;
    Ok(())
}
