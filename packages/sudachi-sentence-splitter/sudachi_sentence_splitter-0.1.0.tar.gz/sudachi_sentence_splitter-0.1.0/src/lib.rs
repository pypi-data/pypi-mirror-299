use pyo3::prelude::*;
use sudachi::sentence_splitter::{SentenceSplitter, SplitSentences};

/// Splits Japanese text into sentences.
#[pyfunction]
fn split_sentences(text: &str) -> PyResult<Vec<String>> {
    let splitter = SentenceSplitter::new();
    let sentences: Vec<String> = splitter
        .split(text)
        .map(|(_, sentence)| sentence.to_string())
        .collect();
    Ok(sentences)
}

/// A Python module implemented in Rust for splitting Japanese sentences.
#[pymodule]
fn sudachi_sentence_splitter(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(split_sentences, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_split_sentences() {
        let text = "これは一つ目の文です。これは二つ目の文です。三つ目の文です。";
        let result = split_sentences(text).unwrap();
        assert_eq!(result.len(), 3);
        assert_eq!(result[0], "これは一つ目の文です。");
        assert_eq!(result[1], "これは二つ目の文です。");
        assert_eq!(result[2], "三つ目の文です。");
    }

    #[test]
    fn test_split_sentences_with_single_sentence() {
        let text = "これは一つの文だけです。";
        let result = split_sentences(text).unwrap();
        assert_eq!(result.len(), 1);
        assert_eq!(result[0], "これは一つの文だけです。");
    }

    #[test]
    fn test_split_sentences_with_empty_input() {
        let text = "";
        let result = split_sentences(text).unwrap();
        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_split_sentences_with_mixed_punctuation() {
        let text = "これは質問文です？これは感嘆文です！最後の文です。";
        let result = split_sentences(text).unwrap();
        assert_eq!(result.len(), 3);
        assert_eq!(result[0], "これは質問文です？");
        assert_eq!(result[1], "これは感嘆文です！");
        assert_eq!(result[2], "最後の文です。");
    }
}
