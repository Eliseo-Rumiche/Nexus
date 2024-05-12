import { send_for_ajax } from "./utils.js";

$('input[type="radio"]').change(function (e) {
  e.preventDefault();
  const worker = $(this).attr("data-worker");
  const status = $(this).val();
  let data = new FormData();
  data.append("worker", worker);
  data.append("status", status);

  send_for_ajax(location.pathname, data, (res) => {});
});
