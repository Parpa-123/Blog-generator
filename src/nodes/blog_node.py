from src.states.blogstate import BlogState
from langchain_core.messages import HumanMessage, SystemMessage
from src.states.blogstate import Blog
class BlogNode:
    def __init__(self,llm):
        self.llm = llm

    def title_creation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            prompt="""
            You are an expert blog content writer. Use Markdown formatting. Generate
            a blog title for the {topic}. This title should be creative and SEO frie
            """

            system_message= prompt.format(topic=state["topic"])

            response = self.llm.invoke(system_message)
            state["title"] = response.content
            return {
                "blog":{
                    "title":response.content
                }
            }

    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            prompt="""
            You are an expert blog content writer. Use Markdown formatting. Generate
            a blog content for the {topic}. This content should be creative and SEO frie
            """

            system_message= prompt.format(topic=state["topic"])

            response = self.llm.invoke(system_message)
            return {
                "blog":{
                    "title" : state["blog"]["title"],
                    "content" : response.content
                }
            }

    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        """

        translation_prompt="""
        Translate the following blog title and content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.

        ORIGINAL TITLE:
        {blog_title}

        ORIGINAL CONTENT:
        {blog_content}

        """

        blog_title=state["blog"]["title"]
        blog_content=state["blog"]["content"]
        messages=[
            HumanMessage(translation_prompt.format(current_language=state["current_language"],
            blog_title=blog_title,
            blog_content=blog_content
            ))
        ]
        translation_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {
            "blog":{
                "title" : translation_content.title,
                "content" : translation_content.content
            }
        }
    
    def route(self,state:BlogState):
        return {"current_language":state["current_language"]}

    def route_node(self,state:BlogState):
        """
        Route the content to the respective translation function.
        """

        if state["current_language"].lower() == "hindi":
            return "hindi"
        elif state["current_language"].lower() == "french":
            return "french"
        else:
            return "english"

