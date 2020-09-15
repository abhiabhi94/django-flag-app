$(function () {
    // search for a blog in the blog list and user profile view
    $("#search-input").keyup(function () {
        var input, filter, titles, ul, a, i;
        input = $("#search-input");
        filter = input.val().toUpperCase();
        a = $("#blog-search a");
        for (i = 0; i < a.length; ++i) {
            if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
                a[i].style.display = "block";
                if ($("#blog-search > div").hasClass("js-hide-div")) {
                    a[i].parentElement.parentElement.parentElement.style.display = "block";
                }
            } else {
                a[i].style.display = "none";
                if ($("#blog-search > div").hasClass("js-hide-div")) {
                    a[i].parentElement.parentElement.parentElement.style.display = "none";
                }
            }
        }
    });

    // image cropper
    $("#id_profile_img").change(function () {
        var file = $(this).val().toLowerCase();
        var ext = file.substring(file.lastIndexOf('.') + 1);
        if ($.inArray(ext, ['jpg', 'jpeg', 'png', 'bmp']) == -1) {
            alert("Please Upload a valid image with the following formats (.jpg, .jpeg, .png, .bmp)");
        }
        else {
            if (this.files && this.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    $("#image").attr("src", e.target.result);
                    $("#modalCrop").modal("show");
                }
                reader.readAsDataURL(this.files[0]);
            }
        }
    });

    // HANDLE THE CROPPER BOX
    var $image = $("#image");
    var cropBoxData;
    var canvasData;
    $("#modalCrop").on("shown.bs.modal", function () {
        $image.cropper({
            viewMode: 1,
            aspectRatio: 1 / 1,
            minCropBoxWidth: 200,
            minCropBoxHeight: 200,
            ready: function () {
                $image.cropper("setCanvasData", canvasData);
                $image.cropper("setCropBoxData", cropBoxData);
            }
        });
    }).on("hidden.bs.modal", function () {
        cropBoxData = $image.cropper("getCropBoxData");
        canvasData = $image.cropper("getCanvasData");
        $image.cropper("destroy");
    });

    // Enable zoom in button
    $(".js-zoom-in").click(function () {
        $image.cropper("zoom", 0.1);
    });

    // Enable zoom out button
    $(".js-zoom-out").click(function () {
        $image.cropper("zoom", -0.1);
    });

    /* SCRIPT TO COLLECT THE DATA AND POST TO THE SERVER */
    $(".js-crop-and-upload").click(function () {
        var cropData = $image.cropper("getData");
        $("#id_x").val(cropData["x"]);
        $("#id_y").val(cropData["y"]);
        $("#id_height").val(cropData["height"]);
        $("#id_width").val(cropData["width"]);
        $("#formUpload").submit();
    });

    var scrollLink = $('.scroll');
    // Smooth scrolling
    scrollLink.click(function (e) {
        e.preventDefault();
        $('body,html').animate({
            scrollTop: $(this.hash).offset().top - 68 //navbar height
        }, 900);
    });
    // search bar
    var i = !1;
    $(".js-search-field").blur(function () {
        i ? ($(".js-search-field").focus(), i = !1) : $(".s-btn").addClass("d-none");
    });
    $(".js-search-field").focus(function () {
        $(".s-btn").removeClass("d-none");
    });
    $(".s-btn").on("mousedown", function () {
        i = !0;
    });

    var prevScroll = $(this).scrollTop();
    $(window).scroll(function () {
        var currentScroll = $(this).scrollTop();
        var authorCard = $(".js-author-card").height() + 48 * 2;
        // hide navbar in blog detail template only
        if (authorCard) {
            if (prevScroll > currentScroll) {
                $(".js-navbar").addClass("fixed-top");
            } else if (prevScroll < currentScroll && currentScroll > authorCard) {
                $(".js-navbar").removeClass("fixed-top");
            }
            prevScroll = currentScroll;
        }

    });

    $(window).on("click touchend touch touchstart", function (e) {
        var navbar = $(".js-navbar")[0];
        if (e.target !== navbar && !navbar.contains(e.target)) {
            $(".js-btn-toggler").addClass("collapsed");
            $("#navbarText").removeClass("show");
        }
    });


    ////////////////////////////////////////////////////////////////////////////////
    // tag input
    var $tagInput = $("#tag-input");
    var $tagList = $(".js-tag");
    var $tagEditor = $(".tag-editor");
    var $formItem = $(".form-item");
    var $tagItem = $(".js-tag li");
    var $tagEditorSpan = $(".tag-editor > span");
    var $option = $('#id_tag option');
    var $selected_option = $('#id_tag option:selected');

    function addTag(tagName) {
        $tagEditorSpan.append('<span class="post-tag">' + tagName +
            '<span class="delete-tag" title="remove this tag"></span></span>');
    }
    function setInputWidth() {
        var tagInputWidth = $tagEditor.width() - $tagEditorSpan.width() - 5;
        $tagInput.attr("style", "width: " + tagInputWidth + "px;");
    }

    // add focus to tag-editor div
    $tagInput.focus(function () {
        $(this).parent('div').addClass("div-focus");
    }).blur(function () {
        $(this).parent('div').removeClass("div-focus");
    });


    // show the hidden tag div (tags list)
    $tagInput.on("keyup keypress", function () {
        // set tag list width
        $tagList.attr("style", "width: " + $formItem.width() + "px;");
        if ($(this).val().replace(/^\s+|\s+$/g, "").length === 0) {
            $tagList.addClass("d-none");
            $(".js-invalid").attr("style", "display: none");
        } else {
            // show tags matching the input value
            var filter = $(this).val().toUpperCase();
            var bool = !1;
            // allow 5 tags only per blog
            if ($tagEditorSpan.children().length < 5) {
                for (var i = 0; i < $tagItem.length; ++i) {
                    if ($tagItem[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
                        bool = !0;
                        $tagItem[i].style.display = "block";
                    } else {
                        $tagItem[i].style.display = "none";
                    }
                }
            } else {
                $(".js-invalid").attr("style", "display: block");
            }
            if (bool) {
                $tagList.removeClass("d-none");
            } else {
                $tagList.addClass("d-none");
            }
        }
    });

    // show selected option in the tag-editor when refreshing or editing
    $selected_option.each(function () {
        addTag($(this).text());
        setInputWidth();
        $tagInput.attr("placeholder", "");
    });

    // add the tag to tag-editor
    $tagItem.on("click touchend", function (e) {
        addTag(e.target.innerHTML);
        setInputWidth();
        $tagList.addClass("d-none");
        $tagInput.val("");

        // select corresponding choice in the hidden field
        $option.each(function () {
            if ($(this).text() === e.target.innerHTML) {
                $(this).prop("selected", true);
            }
        });
        $tagInput.attr("placeholder", "");
        $tagInput.focus();
    });

    // delete tag from tag-editor
    $tagEditor.on("click touchend", ".delete-tag", function (e) {
        var tagName = $(this).parent().text();
        var tagExist = !1;
        $(this).parent().remove();
        $tagInput.focus();
        $(".delete-tag").each(function () {
            if ($(this).parent().text() === tagName) {
                tagExist = !0;
            }
        });
        // check if deleted tag is duplicated
        if (!tagExist) {
            $option.each(function () {
                if ($(this).text() === tagName) {
                    $(this).prop("selected", false);
                }
            });
        }
        setInputWidth();
        if ($(".delete-tag").length === 0) {
            $tagInput.attr("placeholder", "At least one tag (e.g. Python, Django) Maximum 5");
        }

    });


    // resize blog panels to fit the viewport in blog views
    function resizeFun() {
        // blog panels
        var viewportHeight = window.innerHeight;
        var navbarHeight = $(".navbar").height();
        var create_btnHeight = $("#createbtn").height();
        var userHeight = $("#user").height();
        // socila links in home page
        $("#js-social-links").attr("style", "top: " + viewportHeight / 3);

        // 95 margins
        var leftcardHeight = viewportHeight - (navbarHeight + create_btnHeight + userHeight + 91);
        var rightcardHeight = viewportHeight - (navbarHeight + 16);

        $("#left-card").attr("style", "height: " + leftcardHeight + "px;");
        $("#right-card").attr("style", "height: " + rightcardHeight + "px;");
        // tag input and list
        setInputWidth();
        $tagList.attr("style", "width: " + $formItem.width() + "px;");
    };
    resizeFun();
    $(window).resize(resizeFun);

});
