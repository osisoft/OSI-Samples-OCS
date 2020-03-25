package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class Field {
    private FieldSource FieldSource;
    private String[] Keys;
    private String Label;

    public FieldSource getFieldSource() {
        return FieldSource;
    }

    public void setFieldSource(FieldSource fieldSource) {
        this.FieldSource = fieldSource;
    }

    public String[] getKeys() {
        return Keys;
    }

    public void setKeys(String[] keys) {
        this.Keys = keys;
    }

    public String getLabel() {
        return Label;
    }

    public void setLabel(String label) {
        this.Label = label;
    }
}
