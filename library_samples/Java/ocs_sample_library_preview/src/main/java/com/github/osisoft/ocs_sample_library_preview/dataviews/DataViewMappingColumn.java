package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataViewMappingColumn {
    private String Name = "";
    private Boolean IsKey;
    private String DataType = "";
    private DataViewMappingRule MappingRule;

    /** Base constructor */
    public DataViewMappingColumn() {
    }

    /**
     * Constructor
     * 
     */
    public DataViewMappingColumn(String name, Boolean isKey, String dataType, DataViewMappingRule mappingRule) {
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

    public DataViewMappingRule getMappingRule() {
        return MappingRule;
    }

    public void setMappingRule(DataViewMappingRule mappingRule) {
        this.MappingRule = mappingRule;
    }
}
