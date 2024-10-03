"""An XBlock that displays School Yourself reviews and may publish grades."""

import hashlib
import hmac
from six import text_type
import six.moves.urllib.request, six.moves.urllib.parse, six.moves.urllib.error

from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment

from .schoolyourself import SchoolYourselfXBlock


class SchoolYourselfReviewXBlock(SchoolYourselfXBlock):
    """
    This block renders a launcher button for a School Yourself review,
    which is rendered in an iframe. The block transmits the anonymous
    user ID and has a handler that receives information from School
    Yourself regarding the user's progress and mastery through the
    topic being shown.
    """
    has_children = False
    has_score = True
    weight = 1.0

    def get_display_name(self, module_title):
      return "Review: %s" % module_title

    def student_view(self, context=None):
      """
      The primary view of the SchoolYourselfReviewXBlock, shown to students
      when viewing courses.
      """
      # Construct the URL we're going to stuff into the iframe once
      # it gets launched:
      partner_url_params = self.get_partner_url_params(self.shared_key)

      iframe_url_params = dict(partner_url_params)
      iframe_url_params["module"] = self.module_id

      mastery_url_params = dict(partner_url_params)
      mastery_url_params["tags"] = self.module_id

      # Set up the screenshot URL:
      screenshot_url = "%s/page/screenshot/%s" % (self.base_url,
                                                  self.module_id)

      mastery_url = "%s/progress/mastery?%s" % (
          self.base_url, six.moves.urllib.parse.urlencode(mastery_url_params))

      context = {
        "iframe_url": "%s/review/embed?%s" % (
            self.base_url, six.moves.urllib.parse.urlencode(iframe_url_params)),
        "title": self.module_title,
        "icon_url": self.runtime.local_resource_url(self,
                                                    "public/review_icon.png"),
        "mastery_url": mastery_url
      }



      # Now actually render the fragment, which is just a button with
      # some JS code that handles the click event on that button.
      fragment = Fragment(self.render_template("review_student_view.html",
                                               context))

      # Load the common JS/CSS libraries:
      fragment.add_css_url(
        self.runtime.local_resource_url(self, "public/sylib.css"))
      fragment.add_javascript_url(
        self.runtime.local_resource_url(self, "public/sylib.js"))


      # And finally the embedded HTML/JS code:
      fragment.add_javascript(self.resource_string(
          "static/js/review_student_view.js"))
      fragment.add_css(self.resource_string(
          "static/css/student_view.css"))
      fragment.add_css_url("//fonts.googleapis.com/css?family=Open+Sans:700,400,300")
      fragment.initialize_js("SchoolYourselfReviewStudentView")
      return fragment


    @XBlock.json_handler
    def handle_grade(self, data, suffix=""):
      """This is the handler that gets called when we receive grades.

      We will verify the message to make sure that it is signed and
      that the signature is valid. If everything is good, then we'll
      publish a "grade" event for this module.

      The actual work is done in handle_grade_json(), and this method
      just calls that. This method is just here so that it can be wrapped
      by XBlock.json_handler, but the unit test covers the code in
      handle_grade_json() to avoid having to wrap everything around a
      Request/Response object.
      """
      return self.handle_grade_json(data)


    def handle_grade_json(self, data):
      if not isinstance(data, dict):
        return "bad_request"

      mastery = data.get("mastery", None)
      user_id = data.get("user_id", None)
      signature = data.get("signature", None)

      if not mastery or not user_id or not signature:
        return "forbidden"

      # Check that the module ID we care about is actually in the data
      # that was sent.
      mastery_level = mastery.get(self.module_id, None)
      if mastery_level is None:
        return "bad_request"

      try:
        # The mastery level being passed in should be a number, otherwise
        # things later on in this method will choke.
        mastery_level = float(mastery_level)
      except ValueError:
        return "bad_request"

      # Verify the signature.
      sk = self.shared_key
      if isinstance(self.shared_key, str):
        sk = self.shared_key.encode('utf-8')
      verifier = hmac.new(sk, user_id.encode('utf-8'), digestmod='MD5')
      for key in sorted(mastery):
        verifier.update(key.encode('utf-8'))
        # Every entry should be a number.
        try:
          mastery[key] = float(mastery[key])
        except ValueError:
          return "bad_request"

        verifier.update(b"%.2f" % mastery[key])

      # If the signature is invalid, do nothing.
      if signature != verifier.hexdigest():
        return "invalid_signature"

      # If we got here, then everything checks out and we can submit
      # a grade for this module.
      scaled_mastery_level = min(mastery_level / 0.7, 1.0)
      self.runtime.publish(self, "grade",
                           { "value": scaled_mastery_level,
                             "max_value": 1.0 })
      return scaled_mastery_level


    @staticmethod
    def workbench_scenarios():
      """A canned scenario for display in the workbench."""
      return [
        ("SchoolYourselfReviewXBlock",
         """\
            <vertical_demo>
              <schoolyourself_review
                  base_url="https://schoolyourself.org"
                  module_id="algebra/multiplication"
                  module_title="Multiplication, Multiplication, 'Multiplication'"
                  shared_key="edx_test"
                  partner_id="edx_test"
              />
            </vertical_demo>
         """),
        ]
