package com.github.osisoft.ocs_sample_library_preview.dataviews;

public enum DataViewShape {

    Standard("Standard"), Narrow("Narrow");

    private final String DataViewShape;

    private DataViewShape(String id) {
        this.DataViewShape = id;
    }

    public String getValue() {
        return DataViewShape;
    }
}
