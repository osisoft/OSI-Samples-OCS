package com.github.osisoft.ocs_sample_library_preview.dataviews;

import com.github.osisoft.ocs_sample_library_preview.sds.SdsTypeCode;

public class DataMapping {
    private String TargetId;
    private String TargetFieldKey;
    private SdsTypeCode TypeCode;

    public String getTargetId() {
        return TargetId;
    }

    public void setTargetId(String targetId) {
        this.TargetId = targetId;
    }

    public String getTargetFieldKey() {
        return TargetFieldKey;
    }

    public void setTargetFieldKey(String targetFieldKey) {
        this.TargetFieldKey = targetFieldKey;
    }

    public SdsTypeCode getTypeCode() {
        return TypeCode;
    }
}
