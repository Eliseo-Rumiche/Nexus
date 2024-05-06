import { send_for_ajax} from "./utils.js";

$(document).ready(function () {

    $('#modalform').submit(async function (e) {
        e.preventDefault();
        $(".modal-footer button").attr('disabled', true);
        $("#btn-submit").append('<span id="spinner" class="spinner-border spinner-border-sm ml-1"></span>');
        const data = new FormData(this)
        
        await send_for_ajax(window.location.pathname, data, (res) => {
                location.reload() 
            
        })

        $('#spinner').remove();
        $(".modal-footer button").attr('disabled', false);
    });

    $('#Modal').on('hide.bs.modal', event => {
        $('#modalform')[0].reset();
        $('#id').val('');
        $('#action').val('add');
    });


    
});