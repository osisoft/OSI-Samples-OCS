package com.github.osisoft.ocs_sample_library_preview.dataviews;

public enum DataItemResourceType {

    Stream("Stream");

    private final String DataItemResourceType;

    private DataItemResourceType(String id) {
        this.DataItemResourceType = id;
    }

    public String getValue() {
        return DataItemResourceType;
    }
}
