package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataviewMappingRule {
    private String[] PropertyPaths;
    private String GroupRuleId = "";
    private String GroupRuleValue = "";

    /** Base constructor */
    public DataviewMappingRule() {
    }

    /**
     * Constructor
     * 
     * @param propertyPaths
     */
    public DataviewMappingRule(String[] propertyPaths) {
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
