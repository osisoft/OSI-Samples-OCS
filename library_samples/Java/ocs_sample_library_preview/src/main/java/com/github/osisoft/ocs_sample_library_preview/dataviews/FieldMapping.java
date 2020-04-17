package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class FieldMapping {
    private String Id;
    private String Label;
    private FieldKind FieldKind;
    private Integer FieldSetIndex;
    private Integer FieldIndex;
    private DataMapping[] DataMappings;

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getLabel() {
        return Label;
    }

    public void setLabel(String label) {
        this.Label = label;
    }

    public FieldKind getFieldKind() {
        return FieldKind;
    }

    public void setFieldKind(FieldKind fieldKind) {
        this.FieldKind = fieldKind;
    }

    public Integer getFieldSetIndex() {
        return FieldSetIndex;
    }

    public void setFieldSetIndex(Integer fieldSetIndex) {
        this.FieldSetIndex = fieldSetIndex;
    }

    public Integer getFieldIndex() {
        return FieldIndex;
    }

    public void setFieldIndex(Integer fieldIndex) {
        this.FieldIndex = fieldIndex;
    }

    public DataMapping[] getDataMappings() {
        return DataMappings;
    }

    public void setDataMappings(DataMapping[] dataMappings) {
        this.DataMappings = dataMappings;
    }
}
