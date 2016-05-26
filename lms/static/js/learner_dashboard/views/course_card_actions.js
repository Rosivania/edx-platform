;(function (define) {
    'use strict';

    define(['backbone',
            'jquery',
            'underscore',
            'gettext',
            'edx-ui-toolkit/js/utils/html-utils',
            'text!../../../templates/learner_dashboard/course_card_actions.underscore'
           ],
         function(
             Backbone,
             $,
             _,
             gettext,
             HtmlUtils,
             pageTpl
         ) {
            return Backbone.View.extend({
                tpl: HtmlUtils.template(pageTpl),

                events: {
                    'click .enroll-button': 'handleEnroll'
                },

                initialize: function() {
                    this.render();
                },

                render: function() {
                    var filledTemplate = this.tpl(this.model.toJSON());
                    HtmlUtils.setHtml(this.$el, filledTemplate);
                },

                handleEnroll: function(){
                    //Enrollment click event handled here
                }
            });
        }
    );
}).call(this, define || RequireJS.define);
