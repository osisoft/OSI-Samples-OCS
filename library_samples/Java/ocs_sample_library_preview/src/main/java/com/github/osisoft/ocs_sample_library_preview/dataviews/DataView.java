package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataView {
    private String Id = "";
    private String Name = "";
    private String Description = "";
    private DataViewQuery[] Queries;
    private DataViewGroupRule[] GroupRules;
    private DataViewMappings Mappings;
    private DataViewIndexConfig IndexConfig;
    private String IndexDataType = "";

    /** Base constructor */
    public DataView() {
        this.Mappings = new DataViewMappings();
    }

    /**
     * Constructor
     * 
     * @param id            Required
     * @param queries       DataViewQuery[] Required
     * @param groupRules    DataViewGroupRule[] Required
     * @param indexDataType Limited to "DateTime" currently Required
     */
    public DataView(String id, DataViewQuery[] queries, DataViewGroupRule[] groupRules, String indexDataType) {
        this.Id = id;
        this.Queries = queries;
        this.GroupRules = groupRules;
        this.Mappings = new DataViewMappings();
        this.IndexDataType = indexDataType;
    }

    /**
     * Constructor
     * 
     * @param id            Required
     * @param name          not required
     * @param description   not required
     * @param queries       DataViewQuery[] Required
     * @param groupRules    DataViewGroupRule[] Required
     * @param indexDataType Limited to "DateTime" currently Required
     */
    public DataView(String id, String name, String description, DataViewQuery[] queries, DataViewGroupRule[] groupRules,
            String indexDataType) {
        this.Id = id;
        this.Queries = queries;
        this.GroupRules = groupRules;
        this.Mappings = new DataViewMappings();
        this.IndexDataType = indexDataType;
    }

    /**
     * Constructor
     * 
     * @param id            Required
     * @param name          not required
     * @param description   not required
     * @param queries       DataViewQuery[] Required
     * @param groupRules    DataViewGroupRule[] Required
     * @param mappings      DataViewMapping required
     * @param indexConfig   DataViewIndexConfig not require
     * @param indexDataType Limited to "DateTime" currently Required
     */
    public DataView(String id, String name, String description, DataViewQuery[] queries, DataViewGroupRule[] groupRules,
            DataViewMappings mappings, DataViewIndexConfig indexConfig, String indexDataType) {
        this.Id = id;
        this.Name = name;
        this.Description = description;
        this.Queries = queries;
        this.GroupRules = groupRules;
        this.Mappings = mappings;
        this.IndexConfig = indexConfig;
        this.IndexDataType = indexDataType;
    }

    public String getId() {
        return Id;
    }

    public void setId(String id) {
        this.Id = id;
    }

    public String getName() {
        return Name;
    }

    public void setName(String name) {
        this.Name = name;
    }

    public String getDescription() {
        return Description;
    }

    public void setDescription(String description) {
        this.Description = description;
    }

    public DataViewQuery[] getQueries() {
        return Queries;
    }

    public void setQueries(DataViewQuery[] queries) {
        this.Queries = queries;
    }

    public DataViewMappings getMappings() {
        return Mappings;
    }

    public void setMappings(DataViewMappings mappings) {
        this.Mappings = mappings;
    }

    public DataViewIndexConfig getIndexConfig() {
        return IndexConfig;
    }

    public void setIndexConfig(DataViewIndexConfig indexConfig) {
        this.IndexConfig = indexConfig;
    }

    public String getIndexDataType() {
        return IndexDataType;
    }

    public void setIndexDataType(String indexDataType) {
        this.IndexDataType = indexDataType;
    }

    public DataViewGroupRule[] getGroupRules() {
        return GroupRules;
    }

    public void setGroupRules(DataViewGroupRule[] rules) {
        this.GroupRules = rules;
    }
}
