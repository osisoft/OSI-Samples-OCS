package com.github.osisoft.ocs_sample_library_preview.dataviews;

public class ResponseWithLinks {
  private String Response = "";
  private String First;
  private String Next;

  public String getResponse() {
    return Response;
  }

  public void setResponse(String response) {
    this.Response = response;
  }

  public String getFirst() {
    return First;
  }

  public void setFirst(String first) {
    this.First = first;
  }

  public String getNext() {
    return Next;
  }

  public void setNext(String next) {
    this.Next = next;
  }
}