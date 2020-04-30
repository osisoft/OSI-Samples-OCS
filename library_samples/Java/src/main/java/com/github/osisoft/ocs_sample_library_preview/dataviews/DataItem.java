package com.github.osisoft.ocs_sample_library_preview.dataviews;

import java.util.Map;

public class DataItem {
    private String Id;
    private String Name;
    private String Description;
    private String TypeId;
    private DataItemResourceType ResourceType;
    private String[] Tags;
    private Map<String, String> Metadata;
    private DataItemField[] DataItemFields;

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

    public String getTypeId() {
        return this.TypeId;
    }

    public void setTypeId(String typeId) {
        this.TypeId = typeId;
    }

    public DataItemResourceType getResourceType() {
        return ResourceType;
    }

    public void setResourceType(DataItemResourceType resourceType) {
        this.ResourceType = resourceType;
    }

    public String[] getTags() {
        return Tags;
    }

    public void setTags(String[] tags) {
        this.Tags = tags;
    }

    public Map<String, String> getMetadata() {
        return Metadata;
    }

    public void setMetadata(Map<String, String> metadata) {
        this.Metadata = metadata;
    }

    public DataItemField[] getDataItemFields() {
        return DataItemFields;
    }

    public void setDataItemFields(DataItemField[] dataItemFields) {
        this.DataItemFields = dataItemFields;
    }
}
