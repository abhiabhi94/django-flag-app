document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  let headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded'
  };

  const fadeOut = function (element, duration) {
    let interval = 10;//ms
    let opacity = 1.0;
    let targetOpacity = 0.0;
    let timer = setInterval(function () {
      if (opacity <= targetOpacity) {
        opacity = targetOpacity;
        clearInterval(timer);
      }
      element.style.opacity = opacity;
      opacity -= 1.0 / ((1000 / interval) * duration);
    }, interval);
  };

  const fadeIn = function (element, duration) {
    let interval = 20;//ms
    let opacity = 0.0;
    let targetOpacity = 1.0;
    let timer = setInterval(function () {
      if (opacity >= targetOpacity) {
        opacity = targetOpacity;
        clearInterval(timer);
      }
      element.style.opacity = opacity;
      opacity += 1.0 / ((1000 / interval) * duration);
    }, interval);
  };

  const toggleClass = function (element, addClass, removeClass, action) {
    if (action === 'add') {
      element.classList.add(addClass);
      element.classList.remove(removeClass);
    } else {
      element.classList.remove(addClass);
      element.classList.add(removeClass);
    }
  };

  const toggleTitle = function (element, action) {
    const spanEle = element.querySelector('span');
    if (action == 'add') {
      spanEle.title = 'Remove flag';
    } else {
      spanEle.title = 'Report content';
    }
  };

  const createInfoElement = function (responseEle, status, msg, duration = 2) {
    switch (status) {
      case -1:
        status = "danger";
        break;
      case 0:
        status = "success";
        break;
      case 1:
        status = "warning";
        break;
    }
    const cls = 'alert-' + status;
    const temp = document.createElement('div');
    temp.classList.add('h6');
    temp.classList.add('alert');
    temp.classList.add(cls);
    temp.innerHTML = msg;
    responseEle.prepend(temp);
    fixToTop(temp);
    fadeIn(temp, duration);
    setTimeout(() => {
      fadeOut(temp, duration);
    }, duration * 1500);

    setTimeout(() => {
      temp.remove();
    }, 2500 * duration);
  };

  const fixToTop = function (div) {
    const top = 200;
    const isFixed = div.style.position === 'fixed';
    if (div.scrollTop > top && !isFixed) {
      div.setAttribute('style', "{'position': 'fixed', 'top': '0px'}");
    }
    if (div.scrollTop < top && isFixed) {
      div.setAttribute('style', "{'position': 'static', 'top': '0px'}");
    }

  };

  const hideModal = function (modal) {
    modal.style.display = 'none';
    modal.querySelector('form').reset();
    modal.querySelector('textarea').style.display = 'none';
  };

  const showModal = function (e) {
    const modal = e.currentTarget.nextElementSibling;
    modal.style.display = "block";
  };

  const removeFlag = function (e) {
    submitFlagForm(e.currentTarget, 'remove');
  };

  const convertDataToURLQuery = function (data) {
    return Object.keys(data).map(function (key) {
      return encodeURIComponent(key) + '=' + encodeURIComponent(data[key]);
    }).join('&');
  };

  const submitFlagForm = function (ele, action = 'add') {
    let flagEle, info = null, reason = null;
    if (action !== 'add') {
      action = 'remove';
      flagEle = ele;
    } else {
      flagEle = ele.closest('.report-modal-form-combined').firstElementChild;
      reason = ele.querySelector('input[name="reason"]:checked').value;
      info = ele.querySelector('textarea').value;
    }
    const url = flagEle.getAttribute('data-url');
    const appName = flagEle.getAttribute('data-app-name');
    const modelName = flagEle.getAttribute('data-model-name');
    const modelId = flagEle.getAttribute('data-model-id');
    const csrf = flagEle.getAttribute('data-csrf');
    const data = {
      'app_name': appName,
      'model_name': modelName,
      'model_id': modelId,
    };
    if (reason) { data['reason'] = reason; };
    if (info) { data['info'] = info; };
    const query = convertDataToURLQuery(data);
    headers['X-CSRFToken'] = csrf;
    fetch(url, {
      'method': 'post',
      'headers': headers,
      'body': query,
    }).then(function (response) {
      return response.json();
    }).then(function (response) {
      const addClass = 'user-has-flagged';
      const removeClass = 'user-has-not-flagged';
      const flagIcon = flagEle.querySelector('.flag-icon');
      if (response) {
        createInfoElement(flagEle.parentElement, response.status, response.msg);
        const modal = flagEle.nextElementSibling;
        let action;
        if (response.flag === 1) {
          action = 'add';
          hideModal(modal);
          flagEle.removeEventListener('click', showModal);
          flagEle.addEventListener('click', removeFlag);
        } else {
          action = 'remove';
          flagEle.removeEventListener('click', removeFlag);
          flagEle.addEventListener('click', showModal);
          prepareFlagModal(flagEle);
        }
        toggleClass(flagIcon, addClass, removeClass, action);
        toggleTitle(flagEle, action);
      }
    }).catch(function (error) {
      alert('The flagging request could not be processed. Please try again.');
    });
  };

  const prepareFlagModal = function (flagEle, parent = null) {
    if (!parent) {
      parent = flagEle.nextElementSibling.parentElement;
    };
    const modal = parent.querySelector('.flag-report-modal');
    flagEle.addEventListener('click', showModal);
    const span = parent.querySelector(".report-modal-close");
    span.onclick = function () {
      hideModal(modal);
    };
    // when the user clicks on the last reason , open the info box
    const flagForm = parent.querySelector('.report-modal-form');
    const lastFlagReason = flagForm.querySelector('.last-flag-reason');
    const flagInfo = flagForm.querySelector('.report-modal-form-info');
    flagForm.onchange = function (event) {
      if (event.target.value === lastFlagReason.value) {
        flagInfo.required = true;
        flagInfo.style.display = "block";
      } else {
        flagInfo.style.display = "none";
      };
    };
    // add flag
    flagForm.onsubmit = function (event) {
      event.preventDefault();
      submitFlagForm(flagForm, 'add');
    };
  };

  const parents = document.getElementsByClassName("report-modal-form-combined");
  for (const parent of parents) {
    const modal = parent.querySelector('.flag-report-modal');
    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
      if (event.target == modal) {
        hideModal(modal);
      };
    };

    const flagEle = parent.querySelector(".flag-report-icon");
    const flagIcon = flagEle.querySelector('.flag-icon');
    if (flagIcon.classList.contains('user-has-not-flagged')) {
      prepareFlagModal(flagEle, parent);
    } else {
      flagEle.addEventListener('click', removeFlag);
    };
  };
});
