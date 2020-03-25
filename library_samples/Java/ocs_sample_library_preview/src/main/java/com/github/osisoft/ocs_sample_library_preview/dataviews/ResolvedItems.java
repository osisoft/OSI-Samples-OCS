package com.github.osisoft.ocs_sample_library_preview.dataviews;

import java.util.Date;

public class ResolvedItems<T> {
    private T[] Items;
    private Date TimeOfResolution;

    public T[] getItems() {
        return Items;
    }

    public void setItems(T[] items) {
        this.Items = items;
    }

    public Date getTimeOfResolution() {
        return TimeOfResolution;
    }

    public void setTimeOfResolution(Date timeOfResolution) {
        this.TimeOfResolution = timeOfResolution;
    }
}
