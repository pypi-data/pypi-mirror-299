use html2text::{
    render::text_renderer::{TaggedLine, TextDecorator},
    Colour,
};

#[derive(Clone, Debug)]
pub struct CustomDecorator {}

#[derive(PartialEq, Eq, Clone, Debug, Default)]
#[non_exhaustive]
pub enum CustomAnnotation {
    #[default]
    Default,
    Link(String),
    Image(String),
    Emphasis,
    Strong,
    Code,
    Preformat(bool),
    Colour(Colour),
    BgColour(Colour),
}

impl CustomDecorator {
    #[allow(clippy::new_without_default)]
    pub fn new() -> CustomDecorator {
        CustomDecorator {}
    }
}

impl TextDecorator for CustomDecorator {
    type Annotation = CustomAnnotation;

    fn decorate_link_start(&mut self, url: &str) -> (String, Self::Annotation) {
        ("".to_string(), CustomAnnotation::Link(url.to_string()))
    }

    fn decorate_link_end(&mut self) -> String {
        "".to_string()
    }

    fn decorate_em_start(&self) -> (String, Self::Annotation) {
        ("**".to_string(), CustomAnnotation::Emphasis)
    }

    fn decorate_em_end(&self) -> String {
        "**".to_string()
    }

    fn decorate_strong_start(&self) -> (String, Self::Annotation) {
        ("**".to_string(), CustomAnnotation::Strong)
    }

    fn decorate_strong_end(&self) -> String {
        "**".to_string()
    }

    fn decorate_strikeout_start(&self) -> (String, Self::Annotation) {
        ("~~".to_string(), CustomAnnotation::Default)
    }

    fn decorate_strikeout_end(&self) -> String {
        "~~".to_string()
    }

    fn decorate_code_start(&self) -> (String, Self::Annotation) {
        ("`".to_string(), CustomAnnotation::Code)
    }

    fn decorate_code_end(&self) -> String {
        "`".to_string()
    }

    fn decorate_preformat_first(&self) -> Self::Annotation {
        CustomAnnotation::Preformat(false)
    }

    fn decorate_preformat_cont(&self) -> Self::Annotation {
        CustomAnnotation::Preformat(true)
    }

    fn decorate_image(&mut self, src: &str, title: &str) -> (String, Self::Annotation) {
        (
            format!("![{}]({})", title, src),
            CustomAnnotation::Image(src.to_string()),
        )
    }

    fn header_prefix(&self, level: usize) -> String {
        "#".repeat(level) + " "
    }

    fn quote_prefix(&self) -> String {
        "> ".to_string()
    }

    fn unordered_item_prefix(&self) -> String {
        "● ".to_string()
    }

    fn ordered_item_prefix(&self, i: i64) -> String {
        format!("{}. ", i)
    }

    fn finalise(&mut self, _links: Vec<String>) -> Vec<TaggedLine<CustomAnnotation>> {
        Vec::new()
    }

    fn make_subblock_decorator(&self) -> Self {
        CustomDecorator::new()
    }

    fn push_colour(&mut self, colour: Colour) -> Option<Self::Annotation> {
        Some(CustomAnnotation::Colour(colour))
    }

    fn pop_colour(&mut self) -> bool {
        true
    }

    fn push_bgcolour(&mut self, colour: Colour) -> Option<Self::Annotation> {
        Some(CustomAnnotation::BgColour(colour))
    }

    fn pop_bgcolour(&mut self) -> bool {
        true
    }

    fn decorate_superscript_end(&self) -> String {
        "^".to_string()
    }

    fn decorate_superscript_start(&self) -> (String, Self::Annotation) {
        ("^".to_string(), CustomAnnotation::Default)
    }
}
