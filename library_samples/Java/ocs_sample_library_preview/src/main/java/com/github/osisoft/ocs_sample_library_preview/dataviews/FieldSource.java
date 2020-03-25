package com.github.osisoft.ocs_sample_library_preview.dataviews;

public enum FieldSource {

    NotApplicable("NotApplicable"), Id("Id"), Name("Name"), PropertyId("PropertyId"), PropertyName("PropertyName"),
    Tags("Tags"), Metadata("Metadata");

    private final String FieldSource;

    private FieldSource(String id) {
        this.FieldSource = id;
    }

    public String getValue() {
        return FieldSource;
    }
}
