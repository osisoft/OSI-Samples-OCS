package com.github.osisoft.ocs_sample_library_preview.dataviews;

import java.util.Date;

public class ResolvedItem<T> {
    private T Item;
    private Date TimeOfResolution;

    public T getItem() {
        return Item;
    }

    public void setItem(T item) {
        this.Item = item;
    }

    public Date getTimeOfResolution() {
        return TimeOfResolution;
    }

    public void setTimeOfResolution(Date timeOfResolution) {
        this.TimeOfResolution = timeOfResolution;
    }
}
