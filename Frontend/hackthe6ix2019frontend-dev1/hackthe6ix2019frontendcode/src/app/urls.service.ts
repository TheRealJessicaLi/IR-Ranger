import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class UrlsService {

  // regression to local host
  // uri = 'http://ec2-3-17-165-213.us-east-2.compute.amazonaws.com:4000';
  uri = 'http://localhost:4000';

  constructor(private http: HttpClient) { }

  getURL() {
    return this.http.get('${this.uri}/urls');
  }
}
