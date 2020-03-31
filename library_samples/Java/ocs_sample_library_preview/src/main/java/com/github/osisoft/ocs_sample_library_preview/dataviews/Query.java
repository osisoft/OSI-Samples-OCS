package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class Query {
    private String Id;
    private String Value;

    public Query(String id, String value) {
        this.Id = id;
        this.Value = value;
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getValue() {
        return Value;
    }

    public void setValue(String value) {
        this.Value = value;
    }
}
