package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataviewMappingColumn {
    private String Name = "";
    private Boolean IsKey;
    private String DataType = "";
    private DataviewMappingRule MappingRule;

    /** Base constructor */
    public DataviewMappingColumn() {
    }

    /**
     * Constructor
     * 
     */
    public DataviewMappingColumn(String name, Boolean isKey, String dataType, DataviewMappingRule mappingRule) {
        this.Name = name;
        this.IsKey = isKey;
        this.DataType = dataType;
        this.MappingRule = mappingRule;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public Boolean getIsKey() {
        return IsKey;
    }

    public void setIsKey(Boolean isKey) {
        this.IsKey = isKey;
    }

    public String getDataType() {
        return DataType;
    }

    public void setDataType(String dataType) {
        this.DataType = dataType;
    }

    public DataviewMappingRule getMappingRule() {
        return MappingRule;
    }

    public void setMappingRule(DataviewMappingRule mappingRule) {
        this.MappingRule = mappingRule;
    }
}
