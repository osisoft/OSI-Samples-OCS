package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataViewMappings {
    private DataViewMappingColumn[] Columns;

    /** Base constructor */
    public DataViewMappings() {
    }

    /**
     * Constructor
     * 
     * @param columns
     */
    public DataViewMappings(DataViewMappingColumn[] columns) {
        this.Columns = columns;
    }

    public DataViewMappingColumn[] getColumns() {
        return Columns;
    }

    public void setColumns(DataViewMappingColumn[] columns) {
        this.Columns = columns;
    }
}
