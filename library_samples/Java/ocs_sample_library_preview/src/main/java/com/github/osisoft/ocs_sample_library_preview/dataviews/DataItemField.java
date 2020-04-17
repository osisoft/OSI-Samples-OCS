package com.github.osisoft.ocs_sample_library_preview.dataviews;

import com.github.osisoft.ocs_sample_library_preview.sds.SdsTypeCode;

public class DataItemField {
    private String Id;
    private String Name;
    private SdsTypeCode TypeCode;
    private Boolean IsKey;

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

    public SdsTypeCode getTypeCode() {
        return TypeCode;
    }

    public void setTypeCode(SdsTypeCode typeCode) {
        this.TypeCode = typeCode;
    }

    public Boolean getIsKey() {
        return IsKey;
    }

    public void setIsKey(Boolean isKey) {
        this.IsKey = isKey;
    }
}
