package com.github.osisoft.ocs_sample_library_preview.dataviews;

import com.github.osisoft.ocs_sample_library_preview.sds.SdsTypeCode;

public class DataView {
    private String Id;
    private String Name;
    private String Description;
    private Query[] Queries;
    private FieldSet[] DataFieldSets;
    private Field[] GroupingFields;
    private Field IndexField;
    private SdsTypeCode IndexTypeCode;
    private String DefaultStartIndex;
    private String DefaultEndIndex;
    private String DefaultInterval;
    private DataViewShape Shape;

    public DataView(String id, String name, String description) {
        this.Id = id;
        this.Name = name;
        this.Description = description;
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

    public Query[] getQueries() {
        return Queries;
    }

    public void setQueries(Query[] queries) {
        this.Queries = queries;
    }

    public FieldSet[] getDataFieldSets() {
        return DataFieldSets;
    }

    public void setDataFieldSets(FieldSet[] dataFieldSets) {
        this.DataFieldSets = dataFieldSets;
    }

    public Field[] getGroupingFields() {
        return GroupingFields;
    }

    public void setGroupingFields(Field[] groupingFields) {
        this.GroupingFields = groupingFields;
    }

    public Field setIndexField() {
        return IndexField;
    }

    public void setIndexField(Field indexField) {
        this.IndexField = indexField;
    }

    public SdsTypeCode getIndexTypeCode() {
        return IndexTypeCode;
    }

    public void setIndexTypeCode(SdsTypeCode indexTypeCode) {
        this.IndexTypeCode = indexTypeCode;
    }

    public String getDefaultStartIndex() {
        return DefaultStartIndex;
    }

    public void setDefaultStartIndex(String defaultStartIndex) {
        this.DefaultStartIndex = defaultStartIndex;
    }

    public String getDefaultEndIndex() {
        return DefaultEndIndex;
    }

    public void setDefaultEndIndex(String defaultEndIndex) {
        this.DefaultEndIndex = defaultEndIndex;
    }

    public String getDefaultInterval() {
        return DefaultInterval;
    }

    public void setDefaultInterval(String defaultInterval) {
        this.DefaultInterval = defaultInterval;
    }

    public DataViewShape getShape() {
        return Shape;
    }

    public void setShape(DataViewShape shape) {
        this.Shape = shape;
    }
}
