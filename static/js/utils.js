/**
 *
 * @param {Sting} title
 * @param {function} callback
 */
export const confirmation_notification = (title, callback) => {
  Swal.fire({
    title: title,
    text: "",
    icon: "question",
    showCancelButton: true,
    confirmButtonColor: "#3085d6",
    cancelButtonColor: "#d33",
    confirmButtonText: "Sí, Continuar",
    cancelButtonText: "No, Cancelar",
    reverseButtons: true,
  }).then((result) => {
    if (result.isConfirmed) {
      callback();
    }
  });
};

/**
 *
 * @param {String} icon success | error | question | info
 * @param {String} title
 * @param {String} text
 */
export const notification = (icon, title, text) => {
  Swal.fire({
    icon: icon,
    title: title,
    html: text,
  });
};




export const show_simple_datables = (object) => {
  var table = $("#table").DataTable({
    responsive: true,
    language: {
      url: "https://cdn.datatables.net/plug-ins/1.13.1/i18n/es-ES.json",
    },
  });


  $("#table tbody").on("click", "button.btn-edit", function () {
    const id = $(this).attr("data-id");
    const data = new FormData();
    data.append("id", id);
    data.append("action", "detail");

    send_for_ajax(document.location.pathname, data, (res) => {
      $("#action").val("edit");
      $.each(res.data, function (key, value) {
        if (value === true) value = 1;
        if (value === false) value = 0;
        $('[name="' + key + '"]')
          .val(value)
          .trigger("change");
      });

      $("#action").val("edit");
      $("#Modal").modal("show");
    });
  });

  $("#table tbody").on("click", "button.btn-active_disactive", function () {
    const id = $(this).attr("data-id");
    const data = new FormData();
    data.append("id", id);
    data.append("action", "active_disactive");

    confirmation_notification("¿Deseas aplicar esta función?", () => {
      send_for_ajax(window.location.pathname, data, (res) =>
        location.reload()
      );
    });
  });


  $("#table tbody").on("click", "button.btn-deleted", function () {
    const id = $(this).attr("data-id");
    const data = new FormData();
    data.append("id", id);
    data.append("action", "deleted");

    confirmation_notification("Esta accion es irrebercible, ¿Deseas aplicar esta función?", () => {
      send_for_ajax(window.location.pathname, data, (res) =>
        location.reload()
      );
    });
  });

};

export const send_for_ajax = async (url, data, callback) => {
  if (!data.has("csrfmiddlewaretoken")) {
    data.append(
      "csrfmiddlewaretoken",
      $('meta[name="csrf-token"]').attr("content")
    );
  }

  $.ajax({
    type: "POST",
    url: url,
    data: data,
    dataType: "json",
    processData: false,
    contentType: false,
  }).done(function (response) {
    if (!response.hasOwnProperty("error")) {
      callback(response);
    } else {
      const errors = response.error;
      let html = "";
      if (typeof errors == "object") {
        html += "<ol>";
        $.each(errors, function (key, value) {
          if (Array.isArray(value)) {
            html += `<li><p>${key} : ${value} </p></li>`;
          } else {
            html += `<li><p>${key} : <ul>`;

            $.each(value, function (k, v) {
              html += `<li><p>${k} : ${v} </p></li>`;
            });
            html += "</ul>";
          }
        });
        html += "</ol>";
      } else {
        html += errors;
      }
      notification("error", "Error...", html);
    }
  });
};
