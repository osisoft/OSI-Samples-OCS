package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataViewQuery {
    private String Id = "";
    private String Query = "";

    /** Base constructor */
    public DataViewQuery() {
    }

    /**
     * Constructor
     * 
     * @param id
     * @param query
     */
    public DataViewQuery(String id, String query) {
        Id = id;
        Query = query;
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getQuery() {
        return Query;
    }

    public void setQuery(String query) {
        this.Query = query;
    }
}
