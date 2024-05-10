import http from 'k6/http';
import { sleep } from 'k6';
export const options = {
  vus: 200,
  duration: '10s',
};
export default function () {
  http.get('https://banhang.lyhtool.com:8000/check_login_state');
  var random_double = Math.random();
  sleep(2*random_double);
}
