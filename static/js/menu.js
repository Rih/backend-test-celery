import { replaceAll } from './utils.js'
class Menu {
    constructor(baseUrl, modalNamesStr){
        this.PARTIALS = JSON.parse(replaceAll(modalNamesStr, "'", "\""));
        this.BASE_URL = baseUrl;
        this.addListeners();
        this.renderRecords();
    }

    addListeners(){
         const self = this;
        $("button.js-create-btn").on('click', (event) => {
            self.prepareModal({model: 'menu',mode: 'create', modal_container: 'create_container'}, 0)
        });
    }

    addCreateListener(mode){
        const self = this;
        $("body").off("submit", `#${self.PARTIALS[mode].form_id}`);
        $(`#${self.PARTIALS[mode].form_id}`).on("submit", function(e){
            self.saveMenu(e, mode, `${mode}_container`);
        });
        self.initSelect2("#id_meals");
    }

     bindDeleteListener(){
        const self = this;
        self.unbindDeleteListener();
        $("button.js-delete-btn").on("click", (event) => {
            const id = $(event.target).data("rowid");
            self.deleteMenu(id);
        });
    }

    unbindDeleteListener(){
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
            self.addCreateListener(mode);
            self.modalOnClose(partials[mode].modal_id);
        }).fail((result, xhr, x2) => {
            Swal.fire({
              title: 'Modal failed!',
              text: 'Error desconocido',
              icon: 'error',
            });
        });
    }

    prepareModal(params){
        const query = new URLSearchParams(params).toString();
        const url = `${this.BASE_URL}/dashboard/menus/${params.mode}/?${query}`;
        this.openModal(url, {
            modal_container: params.modal_container,
            model_name: params.model,
            mode: params.mode,
        });
    }

    saveMenu(event, mode, modal_container){
        event.preventDefault();
        const self = this;
        const url = `${self.BASE_URL}/api/menus/`;
        const form = $(event.target);
        const data = form.serialize();
        const request = $.ajax(
            {
                url: url,
                method: 'POST',
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
            self.renderRecords();
        });
        request.fail((result, xhr, x2) => {
            const res = JSON.parse(result.responseText);
            if (result.status != 200){
                Swal.fire({
                  title: 'Record failed!',
                  text: res.detail,
                  icon: 'error',
                });
            }

        });
    }

    async deleteMenu(menuId){
        const self = this;
        const { isConfirmed } = await Swal.fire({
          title: 'Deletion!',
          text: 'Do you want to continue',
          icon: 'warning',
          confirmButtonText: 'Yes!'
        });
        const url = `${self.BASE_URL}/api/menus/${menuId}/`;
        if (isConfirmed){
            $.ajax(
                {
                    url: url,
                    method: 'DELETE',
                    dataType: 'application/json',
                }
            ).done((result, xhr, x2) => {
                if(x2.status == 204){
                    //refresh table
                    Swal.fire({
                      title: 'Deletion successful!',
                      text: 'OK!',
                      icon: 'success',
                    });
                    self.renderRecords();
                }
            }).fail((result, xhr, x2) => {
                const res = JSON.parse(result.responseText)
                Swal.fire({
                  title: 'Deletion failed!',
                  text: res.detail,
                  icon: 'error',
                });
            });
        }
    }

    // HTML renders
    renderEmptyCard(){
        return `<div class="alert alert-danger" role="alert">No Menu created yet</div>`;
    }

    renderCardContainer(rows){
        const self = this;
        return rows.map( row => {
            return (`<div class="card">
            <div class="card-header" id="${row.id}">
              <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse${row.id}" aria-expanded="false" aria-controls="collapse${row.id}">
                   Menu day: ${row.scheduled_at}
                </button>
                  <button class="btn btn-danger float-right js-delete-btn" data-rowid="${row.id}">
                      <i class="fa fa-trash" aria-hidden="true" data-rowid="${row.id}"></i>
                  </button>
              </h5>
            </div>
            <div id="collapse${row.id}" class="collapse" aria-labelledby="${row.id}" data-parent="#accordion">
              <div class="card-body">
                  ID: (${row.id})
                <ul>
                    ${self.renderRowMenu(row)}
                </ul>
              </div>
            </div>
          </div>`);
        }).join('');

    }

    renderRowMenu(row){
        return row.meals.map( meal => {
            return `<li>${meal.title}</li>`;
        }).join('');
    }

    initSelect2(target){
        $(target).select2({
            placeholder: 'Choose your meals:',
            allowClear: true,
            tags: true,
        });
    }

    renderRecords(){
        const self = this;
        const url = `${self.BASE_URL}/api/menu-list/`;
        $.ajax(
            {
                url: url,
                method: 'GET',
                dataType: 'json',
            }
        ).done((result, xhr, x2) => {
            if(!result.length){
                $("#accordion").html(self.renderEmptyCard());
                return;
            }
            $("#accordion").html(self.renderCardContainer(result));
            self.bindDeleteListener();
        });
    }

};

export default Menu;