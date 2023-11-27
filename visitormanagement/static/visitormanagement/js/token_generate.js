
const submit_button = document.querySelector("#visitor_add");
const token_download_div = document.querySelector("#token_download");
const token_download_html = document.getElementById("token_download_html")



const visitor_name_input = document.getElementById("visitor_name");
const adress = document.getElementById("visitor_address");
const country_code = document.getElementById("id_visitor_phone_number_0");
const phone_number = document.getElementById("id_visitor_phone_number_1");
const email = document.getElementById("visitor_email");
const organization = document.getElementById("visitor_organization");
const department = document.getElementById("to_which_department");
const employee = document.getElementById("to_employee");
const reason = document.getElementById("visitor_purpose");




function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie('csrftoken');
window.onload = function () {
  token_download_div.style.display = 'none';
};

const token_generate_handler = () => {
  //preventDefault()
  token_download_div.style.display = 'block';
}


function disableSubmitButton(event) {
  setTimeout(function () {
    event.target.disabled = true;
  }, 0);
}

const new_visitor_form_submit_error_modal = (jsonresponse) => {
  const fieldErrors = jsonresponse.field_errors;
  const errorsArray = [];

  for (const field in fieldErrors) {
    const errors = fieldErrors[field];
    errorsArray.push(...errors);
  }

  const modalContent = document.createElement('div');
  modalContent.classList.add('error-modal-content');

  for (let i = 0; i < errorsArray.length; i++) {
    const errorCard = document.createElement('div');
    errorCard.classList.add('error-card');

    const errorText = document.createElement('p');
    errorText.classList.add('error-text');
    errorText.innerText = errorsArray[i];

    errorCard.appendChild(errorText);
    modalContent.appendChild(errorCard);
  }

  Swal.fire({
    title: "Please fix these errors.",
    html: modalContent,
    showCloseButton: true,
    showConfirmButton: false,
    customClass: {
      container: 'error-modal-container',
    },
    onOpen: () => {
      const modalContainer = document.querySelector('.swal2-container');
      modalContainer.classList.add('centered-modal');
    },
  });

  console.log(errorsArray);
};

const visitor_post = async (event) => {
  event.preventDefault()

  const new_visitor_name = visitor_name_input.value;
  const new_adress = adress.value;
  const new_country_code = country_code.value;
  const new_phone = phone_number.value;
  const new_email = email.value;
  const new_organization = organization.value;
  const new_department = department.value;
  const new_employee = employee.value;
  const new_reason = reason.value;

  const phone_number_with_country_code = `${new_country_code}${new_phone}`

  const visitor_obj = {
    visitor_name: new_visitor_name,
    visitor_address: new_adress,
    visitor_phone_number: phone_number_with_country_code,
    visitor_email: new_email,
    visitor_organization: new_organization,
    to_which_department: new_department,
    visitor_purpose: new_reason,
    to_employee: new_employee,


  };
  const data = JSON.stringify(visitor_obj);
  console.log(data)




  try {
    //console.log("this is ok")

    const path = window.location.host
    console.log(path)
    const response = await fetch("https://" + path + "/visitor/api/",
      {
        method: "POST",
        credentials: 'same-origin',
        mode: "cors",
        headers: {
          'X-CSRFToken': csrftoken,
          "Content-type": "application/json",
          "Accept": "*/*",
        },
        body: data,
      });

    if (response.ok) {
      Swal.fire({
        title: 'A new visitor added',

      })
      const jsonResponse = await response.json();
      disableSubmitButton(event)
      //console.log(jsonResponse)
      const token_download_img = document.createElement('img');
      token_download_img.src = "/static/visitormanagement/img/icons8-pdf-48.png";
      token_download_img.height = "50px";
      token_download_img.width = "50px";
      token_download_img.alt = "token download image";
      document.getElementById("download_token_h5").innerText = "Download Token PDF file";
      document.getElementById("download_token_anchor").innerHTML = `${jsonResponse.visitor_name} Token`;
    }
    if (response.status === 400) {
      const errorResponse = await response.json()
      new_visitor_form_submit_error_modal(errorResponse)
      //console.log('400 hit')
      //console.log(errorResponse)


    }
  } catch (error) {
    Swal.fire({
      title: `${error}`,

    })
    console.log(error);

  }


}

submit_button.addEventListener('click', visitor_post);
//submit_button.addEventListener('click', token_generate_handler );


