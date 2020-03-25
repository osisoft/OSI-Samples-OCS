package com.github.osisoft.ocs_sample_library_preview.dataviews;

public enum FieldKind {

    IndexField("IndexField"), GroupingField("GroupingField"), DataField("DataField");

    private final String FieldKind;

    private FieldKind(String id) {
        this.FieldKind = id;
    }

    public String getValue() {
        return FieldKind;
    }
}
