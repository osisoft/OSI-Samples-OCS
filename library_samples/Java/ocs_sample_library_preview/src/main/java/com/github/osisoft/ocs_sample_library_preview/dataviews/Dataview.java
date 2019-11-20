package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class Dataview {
    private String Id = "";
    private String Name = "";
    private String Description = "";
    private DataviewQuery[] Queries;
    private DataviewGroupRule[] GroupRules;
    private DataviewMappings Mappings;
    private DataviewIndexConfig IndexConfig;
    private String IndexDataType = "";

    /** Base constructor */
    public Dataview() {
        this.Mappings = new DataviewMappings();
    }

    /**
     * Constructor
     * 
     * @param id            Required
     * @param queries       DataviewQuery[] Required
     * @param groupRules    DataviewGroupRule[] Required
     * @param indexDataType Limited to "DateTime" currently Required
     */
    public Dataview(String id, DataviewQuery[] queries, DataviewGroupRule[] groupRules, String indexDataType) {
        this.Id = id;
        this.Queries = queries;
        this.GroupRules = groupRules;
        this.Mappings = new DataviewMappings();
        this.IndexDataType = indexDataType;
    }

    /**
     * Constructor
     * 
     * @param id            Required
     * @param name          not required
     * @param description   not required
     * @param queries       DataviewQuery[] Required
     * @param groupRules    DataviewGroupRule[] Required
     * @param indexDataType Limited to "DateTime" currently Required
     */
    public Dataview(String id, String name, String description, DataviewQuery[] queries, DataviewGroupRule[] groupRules,
            String indexDataType) {
        this.Id = id;
        this.Queries = queries;
        this.GroupRules = groupRules;
        this.Mappings = new DataviewMappings();
        this.IndexDataType = indexDataType;
    }

    /**
     * Constructor
     * 
     * @param id            Required
     * @param name          not required
     * @param description   not required
     * @param queries       DataviewQuery[] Required
     * @param groupRules    DataviewGroupRule[] Required
     * @param mappings      DataviewMapping required
     * @param indexConfig   DataviewIndexConfig not require
     * @param indexDataType Limited to "DateTime" currently Required
     */
    public Dataview(String id, String name, String description, DataviewQuery[] queries, DataviewGroupRule[] groupRules,
            DataviewMappings mappings, DataviewIndexConfig indexConfig, String indexDataType) {
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

    public DataviewQuery[] getQueries() {
        return Queries;
    }

    public void setQueries(DataviewQuery[] queries) {
        this.Queries = queries;
    }

    public DataviewMappings getMappings() {
        return Mappings;
    }

    public void setMappings(DataviewMappings mappings) {
        this.Mappings = mappings;
    }

    public DataviewIndexConfig getIndexConfig() {
        return IndexConfig;
    }

    public void setIndexConfig(DataviewIndexConfig indexConfig) {
        this.IndexConfig = indexConfig;
    }

    public String getIndexDataType() {
        return IndexDataType;
    }

    public void setIndexDataType(String indexDataType) {
        this.IndexDataType = indexDataType;
    }

    public DataviewGroupRule[] getGroupRules() {
        return GroupRules;
    }

    public void setGroupRules(DataviewGroupRule[] rules) {
        this.GroupRules = rules;
    }
}
