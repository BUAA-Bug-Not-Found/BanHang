import http from 'k6/http';
import { sleep } from 'k6';
export const options = {
  vus: 9,
  duration: '10s',
};
export default function () {
  http.post("https://banhang.lyhtool.com:8000/blog/getBlogs", "{\"pageno\":1,\"pagesize\":15,\"nowTag\":\"-1\"}")
  var random_double = Math.random();
  sleep(2*random_double);
}
