"use strict";

// Sign Up
// function signup() {
//   const signupName = document.querySelector("#signup__name");
//   const signupId = document.querySelector("#signup__id");
//   const signupPassword = document.querySelector("#signup__password");
//   const signupPasswordRe = document.querySelector("#signup__password--re");

//   console.log(signupName.value);

//   $.ajax({
//     type: "POST",
//     url: "",
//     data: {},
//     success: function (response) {},
//   });
// }

 function signup() {
        let id = $("#signup__id").val();
        let name = $("#signup__name").val();
        let password = $("#signup__password").val();
        let password_re = $("#signup__password--re").val();
        if(password != password_re) {
          alert("비밀번호가 일치 하지 않습니다. ");
          return
        }
        console.log(id,name ,password , password_re);

        $.ajax({
          type: "POST",
          url: "/signUp",
          data: { user_id: id, user_name: name, user_pw: password },
          success: function (response) {
            if (response["result"] == "success") {
              alert("회원가입 성공!");
              window.location.href = "/";
            } else {
              alert("회원가입 실패");
              window.location.reload();
            }
          },
        });
      }



function makeCard() {}

// Modal
document.addEventListener("DOMContentLoaded", () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add("is-active");
  }

  function closeModal($el) {
    $el.classList.remove("is-active");
  }

  function closeAllModals() {
    (document.querySelectorAll(".modal") || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll(".js-modal-trigger1") || []).forEach(
    ($trigger) => {
      const modal = $trigger.dataset.target;
      const $target = document.getElementById(modal);
      // console.log($target);

      $trigger.addEventListener("click", () => {
        openModal($target);
      });
    }
  );

  (document.querySelectorAll(".js-modal-trigger2") || []).forEach(
    ($trigger) => {
      const modal = $trigger.dataset.target;
      const $target = document.getElementById(modal);
      // console.log($target);

      $trigger.addEventListener("click", () => {
        openModal($target);
      });
    }
  );

  // Add a click event on various child elements to close the parent modal
  (
    document.querySelectorAll(
      ".modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button"
    ) || []
  ).forEach(($close) => {
    const $target = $close.closest(".modal");

    $close.addEventListener("click", () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener("keydown", (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) {
      // Escape key
      closeAllModals();
    }
  });
});
