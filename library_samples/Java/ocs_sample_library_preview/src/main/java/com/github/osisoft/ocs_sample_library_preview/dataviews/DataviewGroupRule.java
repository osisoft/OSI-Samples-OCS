package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataviewGroupRule {
    private String Id = "";
    private String Resource = "Streams";
    private String Field = "";
    private String[] Values;

    /** Base constructor */
    public DataviewGroupRule() {
    }

    /**
     * Creates a DataviewGroupRule
     * 
     * @param id
     * @param field
     */
    public DataviewGroupRule(String id, String field) {
        this.Id = id;
        this.Field = field;
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getResource() {
        return Resource;
    }

    public void setResource(String resource) {
        this.Resource = resource;
    }

    public String getField() {
        return Field;
    }

    public void setField(String field) {
        this.Field = field;
    }

    public String[] getValues() {
        return Values;
    }

    public void setValues(String[] values) {
        this.Values = values;
    }
}
