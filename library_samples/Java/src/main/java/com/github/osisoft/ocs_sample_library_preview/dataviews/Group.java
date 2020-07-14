package com.github.osisoft.ocs_sample_library_preview.dataviews;

import java.util.Map;

public class Group {
    private String[] Values;
    private Map<String, DataItem[]> DataItems;

    public String[] getValues() {
        return Values;
    }

    public void setValues(String[] values) {
        this.Values = values;
    }

    public Map<String, DataItem[]> getDataItems() {
        return DataItems;
    }

    public void setDataItems(Map<String, DataItem[]> dataItems) {
        this.DataItems = dataItems;
    }
}
