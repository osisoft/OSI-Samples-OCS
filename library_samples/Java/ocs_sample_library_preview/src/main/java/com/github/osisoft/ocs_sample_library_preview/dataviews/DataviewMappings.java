package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataviewMappings {
    private DataviewMappingColumn[] Columns;
    private DataviewMappingRule[] SharedMappingRules;

    /** Base constructor */
    public DataviewMappings() {
    }

    /**
     * Constructor
     * 
     * @param columns
     */
    public DataviewMappings(DataviewMappingColumn[] columns) {
        this.Columns = columns;
    }

    public DataviewMappingColumn[] getColumns() {
        return Columns;
    }

    public void setColumns(DataviewMappingColumn[] columns) {
        this.Columns = columns;
    }

    public DataviewMappingRule[] getSharedMappingRules() {
        return SharedMappingRules;
    }

    public void setSharedMappingRules(DataviewMappingRule[] sharedMappingRules) {
        this.SharedMappingRules = sharedMappingRules;
    }
}
