package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataViewMappingRule {
    private String[] PropertyPaths;
    private String GroupRuleId = "";
    private String GroupRuleValue = "";

    /** Base constructor */
    public DataViewMappingRule() {
    }

    /**
     * Constructor
     * 
     * @param propertyPaths
     */
    public DataViewMappingRule(String[] propertyPaths) {
        this.PropertyPaths = propertyPaths;
    }

    public String[] getPropertyPaths() {
        return PropertyPaths;
    }

    public void setPropertyPaths(String[] propertyPaths) {
        this.PropertyPaths = propertyPaths;
    }

    public String getGroupRuleId() {
        return GroupRuleId;
    }

    public void setGroupRuleId(String groupRuleId) {
        this.GroupRuleId = groupRuleId;
    }

    public String getGroupRuleValue() {
        return GroupRuleValue;
    }

    public void setGroupRuleValue(String groupRuleValue) {
        this.GroupRuleValue = groupRuleValue;
    }
}
