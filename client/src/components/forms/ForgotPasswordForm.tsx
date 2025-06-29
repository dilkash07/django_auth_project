import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  ForgotPasswordFormValues,
  forgotPasswordSchema,
} from "@/schemas/forgotPassword.schema";
import {
  Form,
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "../ui/input";
import { Button } from "../ui/button";
import { ArrowLeft } from "lucide-react";
import { Link } from "react-router-dom";
import { MdLockReset } from "react-icons/md";

const ForgotPasswordForm = () => {
  const form = useForm<ForgotPasswordFormValues>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: "",
    },
  });

  const onsubmit = (data: ForgotPasswordFormValues) => {
    console.log("Form Data: ", data);
  };

  return (
    <div className="max-w-md mx-auto p-6 rounded-2xl shadow-md bg-white dark:bg-zinc-900">
      <div className="flex flex-col gap-2 items-center mb-6">
        <MdLockReset size={56} />
        <h1 className="text-3xl font-serif italic font-semibold mb-4 text-center">
          Forgot Your Passwrod?
        </h1>
        <p className="text-sm italic text-center">
          Don’t worry, we’ve got you covered. Enter your email below, and we’ll
          send you a link to reset your password. If you can’t access your
          email, please try our account recovery options.
        </p>
      </div>

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onsubmit)} className="space-y-2">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder="john@example.com" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <div className="pt-4">
            <Button type="submit" className="w-full">
              Send Reset Link
            </Button>
          </div>
        </form>
      </Form>

      <div className="mt-4">
        <Link
          to={"/login"}
          className="flex gap-1 items-center justify-center hover:underline"
        >
          <ArrowLeft size={18} /> Back to Login
        </Link>
      </div>
    </div>
  );
};

export default ForgotPasswordForm;
