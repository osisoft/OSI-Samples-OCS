package com.github.osisoft.ocs_sample_library_preview.dataviews;

import java.util.Map;

public class DataGroup {

    private Map<String, Object> Tokens;
    private Object DataItems;

    public Map<String, Object> getTokens() {
        return Tokens;
    }

    public void setTokens(Map<String, Object> tokens) {
        this.Tokens = tokens;
    }

    public Object getDataItems() {
        return DataItems;
    }

    public void setDataItems(Object dataItems) {
        this.DataItems = dataItems;
    }
}
