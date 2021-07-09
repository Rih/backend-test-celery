import { replaceAll } from './utils.js'
class Meal {
    constructor(baseUrl, modalNamesStr){
        this.PARTIALS = JSON.parse(replaceAll(modalNamesStr, "'", "\""));
        this.BASE_URL = baseUrl;
        this.TABLE = $('#dataTable');
        this.TABLE_RENDERED;
        this.addListeners();
        this.createTable();
    }

    addListeners(){
         const self = this;
        $("button.js-create-btn").on('click', (event) => {
            self.prepareModal({model: 'meal',mode: 'create', modal_container: 'create_container'}, 0)
        });
    }

    bindTableEventListener(){
        const self = this;
        $("button.js-edit-btn").on('click', (event) => {
            self.prepareModal(
                {model: 'meal',mode: 'edit', modal_container: 'edit_container'},
                $(event.target).data('rowid')
             )
        });
        $("button.js-delete-btn").on('click', (event) => {
            self.deleteMeal($(event.target).data('rowid'))
        });
    }

    unbindTableEventListener(){
        $("body").off("click", ".js-edit-btn");
        $("body").off("click", ".js-delete-btn");
    }

    openModal(url, params){
        const self = this;
        const { modal_container, mode } = params;
        $.ajax(
            {
                url: url,
                method: 'GET',
            }
        ).done((result, xhr, x2) => {
            $(`#${modal_container}`).html(result);
            $(`#${self.PARTIALS[mode].modal_id}`).modal('show');
            self.addCreateEditListener(mode);
            self.modalOnClose(self.PARTIALS[mode].modal_id);

        }).fail((result, xhr, x2) => {
            Swal.fire({
              title: 'Modal failed!',
              text: 'Error desconocido',
              icon: 'error',
            });
        });
    }


    prepareModal(params, mealId = 0){
        const query = new URLSearchParams(params).toString();
        const url = `${this.BASE_URL}/dashboard/meals/${params.mode}/${mealId}/?${query}`;
        this.openModal(url, {
            modal_container: params.modal_container,
            model_name: params.model,
            mode: params.mode,
        });
    }

    saveMeal(event, mode, modal_container){
        event.preventDefault();
        const self = this;
        const modelId = $(event.target).data('modelId');
        const url = (modelId) ? `${self.BASE_URL}/api/meals/${modelId}/` : `${self.BASE_URL}/api/meals/`;
        const form = $(event.target);
        const data = form.serialize();
        const request = $.ajax(
            {
                url: url,
                method: (modelId) ? 'PUT': 'POST',
                dataType: 'json',
                data: JSON.stringify(data),
            }
        );
        request.done( async(result) => {
            await Swal.fire({
              title: 'Action successful!',
              text: 'OK!',
              icon: 'success',
            });
            $(`#${self.PARTIALS[mode].modal_id}`).modal('hide');
            $(`#${modal_container}`).html('');
            $(".modal-backdrop").remove();
            $("#page-top").removeClass("modal-open");
            self.unbindTableEventListener();
            self.TABLE_RENDERED.ajax.reload();
        });
        request.fail((result, xhr, x2) => {
            const res = JSON.parse(result.responseText);
            if (result.status != 200){
                Swal.fire({
                  title: 'Record failed!',
                  text: res.detail,
                  icon: 'error',
                  allowOutsideClick: false,
                  allowEscapeKey: false,
                });
            }

        });
    }

     async deleteMeal(mealId){
        const self = this;
        const { isConfirmed } = await Swal.fire({
          title: 'Deletion!',
          text: 'Do you want to continue',
          icon: 'warning',
          confirmButtonText: 'Yes!'
        });
        const url = `${self.BASE_URL}/api/meals/${mealId}/`;
        if (isConfirmed){
            $.ajax(
                {
                    url: url,
                    method: 'DELETE',
                    dataType: 'application/json',
                }
            ).done(async (result, xhr, x2) => {
                if(x2.status == 204){
                    //refresh table
                    await Swal.fire({
                      title: 'Deletion successful!',
                      text: 'OK!',
                      icon: 'success',
                      allowOutsideClick: false,
                      allowEscapeKey: false,
                    });
                    self.unbindTableEventListener();
                    self.TABLE_RENDERED.ajax.reload();
                }
            }).fail((result, xhr, x2) => {
                const res = JSON.parse(result.responseText)
                Swal.fire({
                  title: 'Deletion failed!',
                  text: res.detail,
                  icon: 'error',
                  allowOutsideClick: false,
                  allowEscapeKey: false,
                });
            });
        }

    }

    modalOnClose(modalId){
        $(`#${modalId}`).on('hidden.bs.modal', function (e) {
            // do something when this modal window is closed...
            $(".modal-backdrop.fade.show").remove();
        });
    }

    renderEditBtn(id){
        return `<button class="btn btn-primary js-edit-btn" data-rowid="${id}">
            <i class="fa fa-edit" aria-hidden="true" data-rowid="${id}"></i>
        </button>`
    }
    renderDeleteBtn(id){
        return `<button class="btn btn-danger js-delete-btn" data-rowid="${id}">
            <i class="fa fa-trash" aria-hidden="true" data-rowid="${id}"></i>
        </button>`
    }

    addCreateEditListener(mode){
        const self = this;
        $(`#${self.PARTIALS[mode].form_id}`).on("submit", function(e){
            self.saveMeal(e, mode, `${mode}_container`);
        });
    }

    createTable(){
        const self = this;
        const url = `${self.BASE_URL}/api/meals/`;
        self.TABLE_RENDERED = self.TABLE.DataTable({
            "ajax": {
                "url": url,
                "dataType": "json",
                "cache": false,
                "dataSrc": ""
            },
            "columns": [
                {
                    data: 'Title',
                    render: function(data, type, row, meta){
                        return row.title
                    }
                },
                {
                    data: 'Action',
                    render: function(data, type, row, meta){
                        const editBtn = self.renderEditBtn(row.id);
                        const deleteBtn = self.renderDeleteBtn(row.id);
                        return `${editBtn} &nbsp; ${deleteBtn}`
                    }
                },
            ],
            'searching': true,
            "destroy": true,
            "pagination": true,
            "bPaginate": false,
            "formatNumber": function ( toFormat ) {
                return toFormat.toString().replace(
                    /\B(?=(\d{3})+(?!\d))/g, "'"
                    );
            },
            "bLengthChange": false,
            "order": [[ 0, "desc" ]],
            "autoWidth": false,
            "drawCallback": function( settings ) {
                self.bindTableEventListener();
            }
        });
    }
};

export default Meal;