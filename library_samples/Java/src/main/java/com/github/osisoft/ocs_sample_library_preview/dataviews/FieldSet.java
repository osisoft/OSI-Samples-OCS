package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class FieldSet {
    private String QueryId;
    private Field[] DataFields;
    private Field IdentifyingField;

    public String getQueryId() {
        return QueryId;
    }

    public void setQueryId(String queryId) {
        this.QueryId = queryId;
    }

    public Field[] getDataFields() {
        return DataFields;
    }

    public void setDataFields(Field[] dataFields) {
        this.DataFields = dataFields;
    }

    public Field getIdentifyingField() {
        return IdentifyingField;
    }

    public void setIdentifyingField(Field identifyingField) {
        this.IdentifyingField = identifyingField;
    }
}
