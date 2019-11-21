package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class DataViewIndexConfig {

    private Boolean IsDefault = true;
    private String StartIndex = "";
    private String EndIndex = "";
    private String Mode = "";
    private String Interval = "";

    public Boolean getIsDefault() {
        return IsDefault;
    }

    public void setIsDefault(Boolean isDefault) {
        this.IsDefault = isDefault;
    }

    public String getStartIndex() {
        return StartIndex;
    }

    public void setStartIndex(String startIndex) {
        this.StartIndex = startIndex;
    }

    public String getEndIndex() {
        return EndIndex;
    }

    public void setEndIndex(String endIndex) {
        this.EndIndex = endIndex;
    }

    public String getMode() {
        return Mode;
    }

    public void setMode(String mode) {
        this.Mode = mode;
    }

    public String getInterval() {
        return Interval;
    }

    public void setInterval(String interval) {
        this.Interval = interval;
    }
}
