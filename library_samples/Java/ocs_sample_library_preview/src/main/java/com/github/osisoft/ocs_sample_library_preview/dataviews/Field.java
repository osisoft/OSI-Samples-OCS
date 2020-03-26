package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class Field {
    private FieldSource Source;
    private String[] Keys;
    private String Label;

    public Field(FieldSource source, String[] keys, String label) {
        this.Source = source;
        this.Keys = keys;
        this.Label = label;
    }

    public FieldSource getSource() {
        return Source;
    }

    public void setSource(FieldSource source) {
        this.Source = source;
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
