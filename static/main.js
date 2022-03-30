

function logout() {
  // $.ajax({
  //   type: "GET",
  //   url: "/logout",
  //   data: {},
  //   success: function (response) {
  //     if (response["result"] == "success") {
  //       alert("로그아웃 성공!");
  //       window.location.href = "/";
  //     }
  //   },
  // });

  $.removeCookie("token");
  alert("로그아웃 성공!");
  window.location.href = "/";
}

function login() {
  let login_id = $("#login__id").val();
  let login_pw = $("#login__password").val();
  $.ajax({
    type: "POST",
    url: "/login",
    data: { login_id: login_id, login_pw: login_pw },
    success: function (response) {
      if (response["result"] == "success") {
        alert("로그인 성공!");
        $.cookie("token", response["token"]);
        // $.cookie("data", response["data"]);
        window.location.href = "/";
      } else {
        alert("로그인 실패! 아이디와 비밀번호 확인하세요");
      }
    },
  });
}

function idOverlap(){
  let login_id = $("#signup__id").val();

  $.ajax({
    type: "POST",
    url: "/idOverlap",
    data: { log_id: login_id},
    success: function (response) {
      if (response["result"] == "success") {
        alert("사용가능한 아이디입니다!")
      } else if(response["result"] == "overlap"){
        alert("아이디가 중복입니다.");
      }
    },
  });
}


function signup() {
  let id = $("#signup__id").val();
  let name = $("#signup__name").val();
  let password = $("#signup__password").val();
  let password_re = $("#signup__password--re").val();
  if (password != password_re) {
    alert("비밀번호가 일치 하지 않습니다. ");
    return;
  }

  if (
    id.length == 0 ||
    name.length == 0 ||
    password.length == 0 ||
    password_re.length == 0
  ) {
    alert(1);
  }

  $.ajax({
    type: "POST",
    url: "/signUp",
    data: { user_id: id, user_name: name, user_pw: password },
    success: function (response) {
      if (response["result"] == "success") {
        alert("회원가입 성공!");
        window.location.href = "/";
      } else if (response["result"] === "overlap") {
        alert("회원가입 실패");
      } else {
        alert("회원가입 실패");
      }
    },
  });
}

function myprofile(user_id) {
  console.log("sdsad", user_id);
  $.ajax({
    type: "GET",
    url: "/myprofile",
    data: { user_id: user_id },
    success: function (response) {
      console.log("response =>", response);
    },
  });
}

function idOverlap() {
  let login_id = $("#signup__id").val();

  $.ajax({
    type: "POST",
    url: "/idOverlap",
    data: { log_id: login_id },
    success: function (response) {
      if (response["result"] == "success") {
        document.querySelector(".fa-circle-check").style.color = "green";
        alert("사용가능한 아이디입니다.");
        document.querySelector(".signup__complete").removeAttribute("disabled");
      } else if (response["result"] == "overlap") {
        document.querySelector(".fa-circle-check").style.color = "black";
        alert("아이디가 중복입니다.");
        document
          .querySelector(".signup__complete")
          .setAttribute("disabled", true);
      }
    },
  });

  $("#signup__id").on("propertychange change keyup paste input", function(){
    document.querySelector(".fa-circle-check").style.color = "black";
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
      console.log($trigger);

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
