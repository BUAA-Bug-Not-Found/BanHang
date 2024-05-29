import http from 'k6/http';
import { sleep } from 'k6';
export const options = {
  vus: 40,
  duration: '10s',
};
export default function () {
  http.get('https://banhang.lyhtool.com:8000/getQuestions?pageNo=1&pageSize=10');
  var random_double = Math.random();
  sleep(2*random_double);
}
