import { send_for_ajax, confirmation_notification } from "./utils.js";

$(".btn_send_mail").click(function (e) {
  e.preventDefault();
  confirmation_notification(
    "¿Desea enviar notificación de la reunión a los participantes?",
    () => {
      Swal.fire({
        title: "Enviando Mensajes...",
        html: "<i class='bx bx-mail-send bx-flashing' ></i><i class='bx bx-mail-send bx-flashing' ></i><i class='bx bx-mail-send bx-flashing' ></i>",
        timer: 1000,
        timerProgressBar: false,
        didOpen: async () => {
          Swal.stopTimer();
          Swal.showLoading();

          const id = $(this).attr("data-id");
          const data = new FormData();
          data.append("id", id);
          data.append("action", "send_mails");

          await send_for_ajax(location.pathname, data, (res) => {

              Swal.resumeTimer();
          });

        }
      });
    }
  );
});
